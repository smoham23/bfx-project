// this function executes the search via an AJAX call
function runSearch( term ) {
    $('#drug_results1').hide();
    $('#drug_results2').hide();
    $('#check').hide();
    $('tbody').empty();
    
    var frmStr = $('#drug_search').serialize();
    
    $.ajax({
        url: './search.cgi',
        dataType: 'json',
        data: frmStr,
        success: function(data, textStatus, jqXHR) {
            processJSON(data);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            alert("Failed to perform the drug interaction checker! textStatus: (" + textStatus + ") and errorThrown: (" + errorThrown + ")");
        }
    });
}

// this processes a passed JSON structure representing drug interactions 
function processJSON( data ) {
    $('#check').text(data.check);
    $('#drug1').text(data.drug1);
    $('#count1').text(data.count1);
    var next_row_num = 1;
    $.each( data.drugs1, function(i, item) {
        $('#table1').append('<tr><td>'+item.value+'</td></tr>');
    });
            
    $('#drug_results1').show();
    $('#drug2').text(data.drug2);
    $('#count2').text(data.count2);
    $.each( data.drugs2, function(i, item) {
        $('#table2').append('<tr><td>'+item.value+'</td></tr>');
     });
    
    $('#check').show();
    $('#drug_results2').show();
}


$(document).ready(function() {
    $('#input_drug1').autocomplete({
        minLength:2,
        source: './autocomplete.cgi'
    });
    $('#input_drug2').autocomplete({
        minLength:2,
        source: './autocomplete.cgi'
    });
    $('#submit').click( function() {
        runSearch();
        return false;
    });
})
