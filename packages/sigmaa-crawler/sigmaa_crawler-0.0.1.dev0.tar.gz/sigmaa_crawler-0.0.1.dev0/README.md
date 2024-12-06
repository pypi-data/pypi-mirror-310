# SIGMMA Crawler

SIGMMA Crawler es una biblioteca para extraer datos de la plataforma SIGMMA de la Universidad del Caribe.

## Características

- Extracción de datos académicos.
- Soporte para métodos.
- Fácil de usar e integrar.

## Instalación

Puedes instalar la biblioteca usando pip:

```bash
pip install sigmma-crawler
```

## Uso

Aquí tienes un ejemplo básico de cómo usar la biblioteca:

```python
from sigmma_crawler import SigmmaCrawler

crawler = SigmmaCrawler(usuario='matricula', contraseña='contraseña')
datos = crawler.academic_offer()
print(datos)
```

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## Contacto

Para más información, puedes contactar a Kenneth en [kennethdiazgonzalez@hotmail.com](mailto:kennethdiazgonzalez@hotmail.com).
