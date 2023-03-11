function search(element_id){

    var $valselect = $('#'+element_id+'');
    if ($valselect.data('selectator') === undefined) {
        $valselect.selectator({
            showAllOptionsOnFocus: true,
            searchFields: 'value text subtitle right'
        });
    }
}
