
// https://js.cytoscape.org/#extensions 
// https://stackoverflow.com/questions/10086693/resize-on-div-element
function move(e) {
    if ((e.w && e.w !== e.offsetWidth) || (e.h && e.h !== e.offsetHeight)) {
        new Function(e.getAttribute('onresize')).call(e);
    }
    e.w = e.offsetWidth;
    e.h = e.offsetHeight;
}


function adjust_window(obj) {
  SETTINGS["width"] = obj.offsetWidth;
  SETTINGS["height"] = obj.offsetHeight;
  let cy = document.getElementById("cy");
  cy.style.width = SETTINGS["width"] - 5;
  cy.style.height = SETTINGS["height"] - 5;
  network();
}


function adjust_node_size(size) {

}


function network() {
  console.log("MAKING NETWORK");
  document.getElementById("map").style.display = "none";
  let i;
  for (i = 0; i < DATA.length; i += 1) {
    let node = DATA[i];
    if (typeof node.data.source != "undefined") {
      node.data["edgewidth"] = 0.25 * node.data[SETTINGS['scaler']];
      node.data["edgesize"] = node.data[SETTINGS['scaler']];
      console.log("edgeXXX", node, node.data);
    }
  }

  let selected_elements = DATA;
  let node = '';
  let edgewidths = [];
  for (i = 0; i < selected_elements.length; i += 1) {
    node = selected_elements[i];
    if (typeof node.data.source != 'undefined') {
      console.log("edge", node);
      edgewidths.push(node.data[SETTINGS['scaler']]);
    }
  }
  /* The scaler function starts with 1 for the lowest edge width and later increases up to scalemax,
  but we assume edges to be in the range 5 - 100.
  */
  let MIN = Math.min( ...edgewidths ), MAX = Math.max( ...edgewidths );
  let scaler = function(x) {
    return (SETTINGS['scalemax'] - 1) * (x - 5) / (100 - 5) + 1;
  }
  for (i = 0; i < selected_elements.length; i += 1) {
    node = selected_elements[i];
    if (typeof node.data.source != 'undefined') {
      node.data["edgeweight"] = scaler(node.data[SETTINGS['scaler']]);
      node.data["weight"] = node.data["edgeweight"];
      console.log(node.data["edgeweight"], node.data[SETTINGS['scaler']]);
    }
  }

  let cy = cytoscape({
    container: document.getElementById('cy'),
    elements: selected_elements, 
    style: [
      {
        selector: 'node',
        style: {
          'text-border-width': '2px',
          'text-border-color': 'green',
          'text-transform': 'lowercase',
          'text-background-shape': 'rectangle',
          'background-color': 'lightsalmon',
          'label': 'data(label)',
          'text-halign': 'center',
          'text-valign': 'center',
          'shape': 'ellipse',
          'width': SETTINGS['nodewidth'],
          'height': SETTINGS['nodeheight']
        }
      },
      {
        selector: 'edge',
        style: {
          'width': 'data(edgeweight)',
          'line-color': '#ccc',
          'line-opacity': 0.2,
          'label': 'data(edgesize)',
          'text-background-color': '#fff',
          'text-outline-color': '#fff',
          'target-arrow-color': '#000',
          'target-arrow-shape': 'triangle-backcurve',
          'curve-style': 'bezier'
        }
      }
    ],
    // https://blog.js.cytoscape.org/2020/05/11/layouts/
    layout: {
        name: SETTINGS['layout'],
        padding: 1,
        nodeSpacing: 50,
        edgeLengthVal: 100,
        animate: true,
        randomize: true,
        maxSimulationTime: 100,
        boundingBox: {
          x1: 0,
          y1: 0,
          y2: SETTINGS["height"],
          x2: SETTINGS["width"]
        },
        edgeLength: function( e ){
          let w = e.data(SETTINGS['scaler']);
  
          if( w == null ){
            w = 0.5;
          }
  
          return 10 / w;
        }
      }
  });
  
  SETTINGS['cytoscape'] = cy
  cy.on("tap", "node", function(evt){
    cy.nodes().style("background-color", "lightsalmon");
    cy.nodes().style("width", SETTINGS["nodewidth"]);
    cy.nodes().style("height", SETTINGS["nodeheight"]);
    cy.edges().style("line-color", "#ccc");
    let node = evt.cyTarget;
    console.log( 'tapped ', node, evt );
    let block = document.getElementById("infotable");
    let text = "<table>";
    text += "<tr><th>Concept</th>" +
      "<td>" + node.data().label + "</td></tr>" +
      "<tr><th>Incoming Edges</th><td>" + node.indegree() + "</td></tr>" +
      "<tr><th>Outgoing Edges</th><td>" + node.outdegree() + "</td></tr>" +

      "</table>";
    block.innerHTML = text;
    block.style.display = "inline-block";
    node.style("background-color", "cornflowerblue");
    node.style("width", SETTINGS["nodewidth"] * 2);
    node.style("height", SETTINGS["nodeheight"] * 2);
    node.incomers().style("line-color", "crimson");
    node.outgoers().style("line-color", "black");
    document.getElementById("map").innerHTML = "";
    document.getElementById("map").style.border = "2px solid red";
    document.getElementById("map").style.display = "inline-block";
    displayMap([]);
  });
  cy.on("tap", "edge", function(evt){
    cy.nodes().style("background-color", "lightsalmon");
    cy.nodes().style("width", SETTINGS["nodewidth"]);
    cy.nodes().style("height", SETTINGS["nodeheight"]);
    cy.edges().style("line-color", "#ccc");
    cy.edges().style("width", 'data(edgewidth)');
    let node = evt.cyTarget;
    console.log( 'tapped edge ', node, evt );
    let block = document.getElementById("infotable");
    let text = "<p>Affix colexifications from «" + node.data().source + "» to «" + node.data().target + "»:</p>" +
      "<table>" + 
      "<tr>" + 
      "<th>Variety" + " (" + node.data().varieties + ")</th>" + 
      "<th>Language" + " (" + node.data().languages + ")</th>" + 
      "<th>Family" + " (" + node.data().families + ")</th>" + 
      "<th>Colexifier</th><th>Colexified</th></tr>";

    let family_values = node.data()["family_values"].split("//");
    let language_values = node.data()["language_values"].split(" ");
    let variety_values = node.data()["variety_values"].split(" ");
    let colexifier_values = node.data()["colexifier_values"].split("//");
    let colexified_values = node.data()["colexified_values"].split("//");
    let language_table = [];
    for (i = 0; i < variety_values.length; i += 1) {
        language_table.push([
          variety_values[i], 
          language_values[i], 
          family_values[i], 
          colexifier_values[i],
          colexified_values[i]
        ]);
    }
    language_table.sort(function (x, y){ return (x[2] + x[1]).localeCompare((y[2] + y[1])); });
    let coords = [];
    for (i = 0; i < language_table.length; i += 1) {
      text += "<tr>" + 
        "<td>" + '<a href="LanguageTable?cldf_id=' + language_table[i][0] + '">' + language_table[i][0] + "</td>" +
        "<td>" + '<a href="LanguageTable?cldf_glottocode=' + language_table[i][0] + '">' + language_table[i][1] + "</a></td>" + 
        "<td>" + '<a href="LanguageTable?Family=' + language_table[i][2] + '">' + language_table[i][2] + "</td>" + 
        "<td>" + plotWord(language_table[i][3]) + "</td>" + 
        "<td>" + plotWord(language_table[i][4]) + "</td>" +
        "</tr>";
      coords.push(LANGS[language_table[i][0]]);
    }
    text += '</table>';
    block.innerHTML = text;
    block.style.display = 'inline-block';

    node.style("line-color", "cornflowerblue");
    node.style("width", node.data().edgewidth * 1.25);

    /* get language map */
    document.getElementById("map").innerHTML = "";
    document.getElementById("map").style.border = "2px solid red";
    document.getElementById("map").style.display = "inline-block";
    displayMap(coords);
  });
};


function displayMap(coords){
  var g = d3.select("#map")
    .append("svg:svg")
    .attr("width", SETTINGS["mapwidth"])
    .attr("height", SETTINGS["mapheight"])
    .append("g");
  var mapPoly = g.append('g').attr('class','mapPoly'); // for the map
  var allCircles = g.append('g').attr('class','allCircles'); // all locations
  var nodeCircles = g.append('g').attr('class','nodeCircles') // for the 
  // locations
  var countrydata = topojson.object(topology,
    topology.objects.countries).geometries;
  mapPoly.selectAll("path")
    .data(topojson.object(topology, topology.objects.countries) 
      .geometries) 
    .enter() 
    .append("path")
    .attr("d", path) 
    .style("fill", "#c0c0c0")
    .style('stroke', 'white')
    .style('stroke-width', function(d){
      return 0;
    })
  ; 

  //console.log(coords);
  allCircles.selectAll("circle") 
    .data(coords) 
    .enter() 
    .append("circle") 
    .attr("class","alllocation")
    .attr("cx", function(d) {
      return projection([d[0], d[1]])[0];
    })
    .attr('cy', function(d){
      return projection([d[0], d[1]])[1]; 
    }) 
    .attr("r", function(d){
      return 3;
    })
    .style("stroke", "white")
    .style("stroke-width", 0.5)
    .style("fill", 'red') 
  ;
}


async function download(event) {
  event.preventDefault();
  let button = document.createElement("a");
  const jpgBlob = await SETTINGS['cytoscape'].jpg();
  button.href = jpgBlob;
  button.download = 'clips.jpg';
  button.click();
  document.body.removeChild(button);
  delete button;
}
