<p align="center">
   <img src="./src/msplotly/images/logo.png" alt="MSPlotly" width="250">
</p>

# Make a graphical representation of BLASTn alignments

Multiple Sequence Plotter with Plotly (MSPlotly) uses GenBank files (.gb) to align the sequences and plot the genes. MSPlotly uses the information from the `CDS` features section to plot the genes. To customize the colors for plotting genes, you can add a `Color` tag in the `CDS` features with a color in hexadecimal. For example, add the tag `/Color="#00ff00"` to show a green gene. Or, you can edit the colors interactively in the plot.

MSPlotly is a user-friendly interactive option for people with little coding knowledge or problems running the classic app `easyfig.` The program runs as a web browser app implemented with `Dash-Plotly.` MSPlotly is a flexible app that allows you to export your graph in different formats and sizes for publication.

## Requirements

- [blastn](https://www.ncbi.nlm.nih.gov/books/NBK569861/) must be installed
  locally and in the path

MSPlotly has been tested in Chrome using macOS.

## Installation

First, create a virtual environment with `conda` or `venv`. Then, install
msplotly using pip as follows:

```bash
pip install git+https://github.com/ivanmugu/msplotly.git
```

## Usage

To run the app type:

```bash
msplotly
```

Output:
<p align="center">
   <img src="./src/msplotly/images/MSPlotly_app.png" alt="MSPlotly" width="600">
</p>


## Credits

Inspired by easyfig: Sullivan et al (2011) Bioinformatics 27(7):1009-1010

## License

BSD 3-Clause License

## Notes

I am developing MSPlotly in my free time, so if you find a bug, it may take me some time to fix it. However, I will fix the problems as soon as possible. Also, if you have any suggestions, let me know, and I will try to implement them.