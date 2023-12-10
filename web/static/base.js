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