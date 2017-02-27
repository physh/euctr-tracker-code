function hide_datatable() {
    /* Hide while loading to prevent style change jitter */
    $('#sponsor_table').hide()
    $('#sponsor_table_loading').show()
    $('#sponsor-pills').hide()
}

function activate_datatable() {
    var t = $('#sponsor_table').DataTable({
        "order": [[ 4, "desc" ]],
	"paging": false,
	"aoColumns": [
	    { "orderSequence": [ "asc", "desc" ] },
	    { "orderSequence": [ "desc", "asc" ], "className": "dt-right" },
	    { "orderSequence": [ "desc", "asc" ], "className": "dt-right"  },
	    { "orderSequence": [ "desc", "asc" ], "className": "dt-right"  },
	    { "orderSequence": [ "desc", "asc" ], "className": "dt-right"  },
	    { "orderSequence": [ "asc", "desc" ] }, // Hidden column
	]
    });

    var show_all = function() {
	t.search("")
	t.columns(5).search("").draw()
	$('#all_sponsors').addClass('active')
	$('#major_sponsors').removeClass('active')
	return false
    }
    $('#all_sponsors').on('click', show_all)
    var show_major = function() {
	t.search("")
	t.columns(5).search("major").draw()
	$('#major_sponsors').addClass('active')
	$('#all_sponsors').removeClass('active')
	return false
    }
    $('#major_sponsors').on('click', show_major)
    show_major();

    t.on('search.dt', function () {
	if (t.search() == "") {
	    $('#all_sponsors').addClass('active')
	    $('#major_sponsors').removeClass('active')
	} else {
	    $('#all_sponsors').removeClass('active')
	    $('#major_sponsors').removeClass('active')
	}
    } );

    /* Show after style change */
    $('#sponsor_table_loading').hide()
    $('#sponsor-pills').show()
    $('#sponsor_table').show()
}


