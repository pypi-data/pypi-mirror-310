# docx2md

Convert _simple_ `.docx` files to markdown.

## Usage: Python

```
import docx2markdown 

# .docx -> .md
docx2markdown.docx_to_markdown("test-text.docx", "test-text-1.md")

# .md -> .docx
docx2markdown.markdown_to_docx("test-text-1.md", "test-text-2.docx")
```

## Usage: Terminal

```
docx2markdown test-text.docx test-text.md
```
OR:
```
docx2markdown test-text.md test-text.docx
```


## Installation

```
pip install docx2markdown
```

## Contributing

Feedback and contributions are welcome! Just open an issue and let's discuss before you send a pull request. 

## Acknowledgements

We acknowledge the financial support by the Federal Ministry of Education and Research of Germany and by Sächsische Staatsministerium für Wissenschaft, Kultur und Tourismus in the programme Center of Excellence for AI-research „Center for Scalable Data Analytics and Artificial Intelligence Dresden/Leipzig", project identification number: ScaDS.AI
