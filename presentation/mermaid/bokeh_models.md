graph LR
    subgraph Bokeh
    python(Python Objects)
    end
    subgraph BokehJS
    javascript(Javascript Objects)
    end
    output(HTML Canvas/SVG Output)
    python-- JSON -->javascript
    javascript-->output
