from IPython.display import display, HTML
import matplotlib.pyplot as plt
import seaborn as sns
from langdetect import detect, DetectorFactory

plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = 'DejaVu Sans'

DetectorFactory.seed = 0

LANGUAGE_MAP = {
    'es': 'Español', 'en': 'Inglés', 'pt': 'Portugués', 'it': 'Italiano',
    'fr': 'Francés', 'de': 'Alemán', 'nl': 'Neerlandés', 'da': 'Danés',
    'ro': 'Rumano', 'tl': 'Tagalo', 'ca': 'Catalán', 'et': 'Estonio',
    'no': 'Noruego', 'fi': 'Finés', 'hu': 'Húngaro', 'tr': 'Turco',
    'lt': 'Lituano', 'sy': 'Sirio', 'sq': 'Albanés', 'sv': 'Sueco',
    'id': 'Indonesio', 'sl': 'Esloveno', 'cs': 'Checo', 'so': 'Somalí',
    'sw': 'Suajili'
}

def apply_plot_config(func):
    """
    Decorador que asegura la configuración correcta de matplotlib antes de graficar.
    """
    import matplotlib.pyplot as plt

    def wrapper(*args, **kwargs):
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['font.family'] = 'DejaVu Sans'
        return func(*args, **kwargs)
    
    return wrapper


def show_image(url, width=1600):
    """
    Displays an image from a URL in a Jupyter notebook.
    """
    display(HTML(f"<img src='{url}' width={width}>"))

@apply_plot_config
def plot_histo(df, variable):
    plt.figure(figsize=(10, 5))
    sns.histplot(df[variable], bins=50, color='skyblue', kde=True)
    plt.title('Histograma: Distribución de ' + variable)
    plt.xlabel('Cantidad de caracteres')
    plt.ylabel('Frecuencia')
    plt.show()

@apply_plot_config
def plot_comments_by_time(df, time_column='time', period='M', color='lightcoral'):
    """
    Distribución de comentarios por periodo temporal.
    
    Parámetros:
    - time_column: columna ya en formato datetime.
    - period: 'M' para mes, 'Y' para año.
    """
    comments_by_period = df[time_column].dt.to_period(period).value_counts().sort_index()
    
    plt.figure(figsize=(12, 6))
    comments_by_period.plot(kind='bar', color=color)
    plt.title(f'Distribución de comentarios por {"mes" if period == "M" else "año"}')
    plt.xlabel('Periodo')
    plt.ylabel('Cantidad de comentarios')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

@apply_plot_config
def plot_correlation_scatter(df, x_var, y_var, color='blue', alpha=0.5):
    """
    Scatterplot entre dos variables numéricas.
    
    Parámetros:
    - x_var: nombre de la columna para el eje X.
    - y_var: nombre de la columna para el eje Y.
    - alpha: transparencia de los puntos.
    """
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x=x_var, y=y_var, color=color, alpha=alpha)
    plt.title(f'Relación entre {x_var.capitalize()} y {y_var.capitalize()}')
    plt.xlabel(x_var.capitalize())
    plt.ylabel(y_var.capitalize())
    plt.grid(True)
    plt.show()

@apply_plot_config
def plot_language_distribution(comment_series, sample_size=500, color='mediumseagreen'):
    """
    Detecta y grafica la distribución de idiomas en una muestra de comentarios.
    
    Parámetros:
    - comment_series: Serie de texto (columna de comentarios).
    - sample_size: número de muestras aleatorias a analizar.
    """
    sample = comment_series.dropna().astype(str)
    sample = sample[sample.apply(lambda x: len(x.strip()) > 10)]
    sample = sample.sample(n=sample_size, random_state=42)
    
    languages = sample.apply(lambda x: detect(x))
    lang_counts = languages.value_counts()
    lang_counts.index = lang_counts.index.map(lambda code: LANGUAGE_MAP.get(code, code))
    
    plt.figure(figsize=(10, 5))
    lang_counts.plot(kind='bar', color=color)
    plt.title('Distribución de idiomas en muestra de comentarios')
    plt.xlabel('Idioma detectado')
    plt.ylabel('Cantidad')
    plt.grid(True)
    plt.show()
