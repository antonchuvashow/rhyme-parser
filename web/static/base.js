//
// // Set up the layout settings
// var layout = d3.layout.cloud()
//     .size([800, 400]) // Set the size of the word cloud container
//     .words(words)
//     .padding(5) // Adjust padding between words
//     .rotate(function () {
//         return ~~(Math.random() * 2) * 90;
//     })
//     .fontSize(function (d) {
//         return d.size;
//     }) // Set the font size based on data size
//     .on("end", draw);
//
// // Function to draw the word cloud
// function draw(words) {
//     var svg = d3.select("#word-cloud-container").append("svg")
//         .attr("width", layout.size()[0])
//         .attr("height", layout.size()[1])
//         .append("g")
//         .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")");
//
//     svg.selectAll("text")
//         .data(words)
//         .enter().append("text")
//         .style("font-size", function (d) {
//             return d.size + "px";
//         })
//         .style("fill", getRandomColor)
//         .style("font-family", "Impact")
//         .attr("text-anchor", "middle")
//         .attr("transform", function (d) {
//             return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
//         })
//         .text(function (d) {
//             return d.text;
//         })
//         .on("click", function (d) {
//             console.log("click");
//             submitForm(d.text);
//         });
// }
//
// // Function to generate a random color
// function getRandomColor() {
//     var hue = Math.floor(Math.random() * 360);
//     var pastel = 'hsl(' + hue + ', 60%, 40%)';
//     return pastel;
// }
//
function submitForm(word) {
    console.log(word);
    // Check if the form and input elements exist
    var form = document.getElementById("search-form");
    var input = document.getElementById("searchform-name");
    var container = document.getElementById("word-cloud-container")

    if (form && input) {
        // Set the input value to the clicked word
        input.value = word;

        // Submit the form
        form.submit();
        container.remove()
    } else {
        console.error("Form or input element not found.");
    }
}

//
// layout.start();


function wordCloud(selector, width, height) {

    var fill = d3.schemeTableau10;

    var svg = d3.select(selector)
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    function draw(words) {
        var cloud = svg.selectAll("g text")
            .data(words, function (d) {
                return d.text;
            })

        cloud.enter()
            .append("text")
            .style("font-family", "Impact")
            .style("fill", function (d, i) {
                if (d.title === 0) {
                    return fill[i % 10];
                } else {
                    return "0"
                }
            })
            .attr("text-anchor", "middle")
            .attr("class", function (d, i) {
                if (d.title === 1) {
                    return "text-title";
                } else {
                    return "words"
                }
            })
            .attr('font-size', 1)
            .text(function (d) {
                return d.text;
            });

        cloud.transition()
            .duration(600)
            .style("font-size", function (d) {
                return d.size + "px";
            })
            .attr("transform", function (d) {
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
            })
            .style("fill-opacity", 1);

        cloud.exit()
            .transition()
            .duration(200)
            .style('fill-opacity', 1e-6)
            .attr('font-size', 1)
            .remove();

        cloud.on("click", function (d) {
            if (d.title === 0) {
                console.log("click");
                submitForm(d.text);
            }
        });
    }

    return {
        update: function (words) {
            d3.layout.cloud().size([width, height])
                .words(words)
                .padding(3)
                .rotate(function () {
                    return ~~(Math.random() * 2) * 90;
                })
                .font("Impact")
                .fontSize(function (d) {
                    return d.size;
                })
                .on("end", draw)
                .start();
        }
    }

}

function showNewWords(vis, i) {
    i += 1
    vis.update(top_searches)
    setTimeout(function () {
        showNewWords(vis)
    }, 5000)
}

var myWordCloud = wordCloud('#word-cloud-container', window.window.innerWidth * 0.6, 500);
myWordCloud.update(top_searches);
myWordCloud.update(top_searches);
// showNewWords(myWordCloud);