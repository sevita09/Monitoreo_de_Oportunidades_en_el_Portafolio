import pandas as pd
import yfinance as yf
import time

def descargar_serie(ticker, start, end, max_reintentos=3):
    """Descarga una serie de precios usando yfinance con reintentos.

    Devuelve (DataFrame, last_err_msg). El DataFrame ya está limpiado con dropna().
    """
    data = pd.DataFrame()
    last_err_msg = ''
    for attempt in range(max_reintentos):
        try:
            data = yf.download(
                ticker,
                start=start,
                end=end + pd.Timedelta(days=1),
                progress=False,
                threads=False,
                multi_level_index=False,
            )
            if not data.empty and 'Close' in data.columns:
                break
        except Exception as e:
            msg = f"Error descargando {ticker} (intento {attempt + 1}/{max_reintentos})"
            return None, msg
        time.sleep(0.5)
    data = data.dropna()
    return data, None

def preparar_serie_denominador_dolar_mep(ggal_ba_df, ggal_df, target_index):
    """Dado dataframes para GGAL.BA y GGAL, devuelve una Serie 'denom' alineada (GGAL.BA*10 / GGAL) reindexada a target_index.

    Lanza ValueError si no hay fechas solapadas.
    """
    ggal_ba_series = ggal_ba_df['Close'] * 10
    ggal_series = ggal_df['Close']
    ggal_ba_series.name = 'GGAL.BA'
    ggal_series.name = 'GGALD.BA'
    denom_df = pd.concat([ggal_ba_series, ggal_series], axis=1, join='inner')
    if denom_df.empty:
        raise ValueError("No hay fechas solapadas entre GGAL.BA y GGALD.BA")
    denom_series = denom_df['GGAL.BA'] / denom_df['GGALD.BA']
    denom_series = denom_series.replace(0, pd.NA)
    denom_aligned = denom_series.reindex(target_index).ffill().bfill()
    return denom_aligned

def calcular_dolar_mep_para_dolarizar(start, end, target_index, max_reintentos=3):
    """Calcula la serie del dólar MEP usando GGAL.BA y GGALD.BA.

    Devuelve (serie_denom_aligned, '') en caso exitoso o (None, mensaje_error) si falla alguna descarga o el proceso.
    """
    ggal_ba, err1 = descargar_serie('GGAL.BA', start, end, max_reintentos=max_reintentos)
    if err1 or ggal_ba.empty:
        return None, f"Error descargando GGAL.BA: {err1 or 'sin datos'}"

    ggal, err2 = descargar_serie('GGALD.BA', start, end, max_reintentos=max_reintentos)
    if err2 or ggal.empty:
        return None, f"Error descargando GGALD.BA: {err2 or 'sin datos'}"

    try:
        denom_aligned = preparar_serie_denominador_dolar_mep(ggal_ba, ggal, target_index)
        return denom_aligned, ''
    except Exception as e:
        return None, str(e)

def dolarizar_serie_mep(ticker, start, end, max_reintentos=3):
    """Dolariza una serie dividiéndola por el dolar mep.

    Ambas series deben estar alineadas en fechas.
    """
    try:
        data, _ = descargar_serie(ticker, start, end, max_reintentos)
    except Exception as e:
        msg = f"No se pudo descargar {ticker} tras {max_reintentos} intentos."
        return None, msg

    try:
        dolar_mep, _ = calcular_dolar_mep_para_dolarizar(start, end, data.index, max_reintentos)
    except Exception as e:
        msg = f"No se pudo calcular el dólar MEP para dolarizar {ticker}"
        return None, msg
    
    close_series = data['Close']
    if isinstance(close_series, pd.DataFrame):
        close_series = close_series.iloc[:, 0]
    close = close_series.reindex(dolar_mep.index).div(dolar_mep)
    if close.dropna().empty:
        msg = f"La conversión a dólares falló por falta de datos coincidentes."
        return None, msg
    
    return close, None