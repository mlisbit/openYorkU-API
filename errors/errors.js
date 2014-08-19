function extract_dup_key(x) {
	return null
}

exports.handle = function(err){
	var err_template = {
		message: null,
		status_code: null,
		detail: null,
		suggestion: null
	}

	if (err.code === 11000) {
		err_template.message = 'Attemped to add entry with non-unique key'
		err_template.suggestion = "Please retry with different '" + extract_dup_key(err.err) + "' value"
	}

	return err_template
}