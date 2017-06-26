$(function() {
// configure typeahead
    $("#out").typeahead({
        highlight: false,
        minLength: 1
    },
    {
        display: Handlebars.compile(                
                "{{City}}, {{District}}, {{Region}}"               
            ),
        limit: 20,
        source: search,
        templates: {
            suggestion: Handlebars.compile(
                "<div>" +
                "<div>{{City}}, {{District}}, {{Region}}</div>" +
                "</div>"
            )
        }
    });
    $("#in").typeahead({
        highlight: false,
        minLength: 1
    },
    {
        display: Handlebars.compile(                
                "{{City}}, {{District}}, {{Region}}"               
            ),
        limit: 20,
        source: search,
        templates: {
            suggestion: Handlebars.compile(
                "<div>" +
                "<div>{{City}}, {{District}}, {{Region}}</div>" +
                "</div>"
            )
        }
    });
    // re-center map after place is selected from drop-down
    $("#out").on("typeahead:selected", function(eventObject, suggestion, name) {
    //suggestion.city.replace("&#x27;","'");    
    //console.log(suggestion.City.replace("'","'"));
    });

   
    
});
    
    
/**
 * Searches database for typeahead's suggestions.
 */

function search(query, syncResults, asyncResults)
{
    // get places matching query (asynchronously)
    //console.log(query);

    var parameters = {
        q: query
    };
    
    $.getJSON(Flask.url_for("search"), parameters)
    .done(function(data, textStatus, jqXHR) {
     
        // call typeahead's callback with search results (i.e., places)
        asyncResults(data);
    })
    .fail(function(jqXHR, textStatus, errorThrown) {

        // log error to browser's console
        console.log(errorThrown.toString());

        // call typeahead's callback with no results
        asyncResults([]);
    });
}
