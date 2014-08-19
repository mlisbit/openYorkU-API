exports.api_ify =function api_ify(data, req, res, next) {
	var output = {
		meta: {
			status: 0,
			timestamp: 0,
			message: '',
		},
		data: {}
	}

	if (data.err) {
		var temp_output = errors.handle(data.err)
		output.meta.message = temp_output.message || data.err.toString()
		output.meta.suggestion = temp_output.suggestion
		output.meta.detail = temp_output.detail || data.err

		output.meta.status = 400;
	} else {
		output.meta.status = data.status || 200;
		output.meta.message = data.message || "Request successful";
		output.data = data.data || {}
	}
	res.status(output.meta.status).json(output)
}