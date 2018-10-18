graph LR
    server[Bokeh Server]
    application[Application]
    server-->application
    application-->d1
    application-->d2
    subgraph User Session
    d1[Python Objects]
    c1[Javascript Objects]
    d1-- WS -->c1
    c1-- WS -->d1
    d1-- JSON -->c1
    end
    c1-->o1[HTML Canvas/SVG Output]
    subgraph User Session
    d2[Python Objects]
    c2[Javascript Objects]
    d2-- WS -->c2
    c2-- WS -->d2
    d2-- JSON -->c2
    end
    c2-->o2[HTML Canvas/SVG Output]
