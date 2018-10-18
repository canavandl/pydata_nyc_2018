Developing Dashboard Applications with Bokeh
PyData NYC 2018
Luke Canavan

View the RevealJS slides simply by opening the presentation/index.html file
in a browser. The presentation contains the required JS and CSS resources and
should be viewable without an internet connection.

#### Installing the App dependencies

Create a conda environment containing the app dependencies using the adjacent
environment.yml file via ```conda env create -f app/environment.yml```

Then activate via ```conda activate pydata_nyc```

#### Running the app

Start the app from the repository root directory via ```bokeh serve app --show```

### Rebuilding the MermaidJS flowcharts

Install mermaid JS and use:

```
npx mmdc -i mermaid/{filename}.md -o lib/images/{filename}.svg -w 1024 -H 768 -b transparent -t dark
```
