from flask import Flask, request, make_response, send_from_directory, jsonify
from dbhelpers import run_procedure
from apihelpers import check_endpoint_info, save_file
import dbcreds


app = Flask(__name__)

@app.post('/api/image')
def post_image():
    # Checking to see if the request.form contains the needed description
    # You might have different fields required for your upload
    is_valid = check_endpoint_info(request.form, ['description'])
    if(is_valid != None):
        return make_response(jsonify(is_valid), 400)

    # Use request.files to make sure the uploaded_image is there
    # Again you can call it whatever you would like
    is_valid = check_endpoint_info(request.files, ['uploaded_image'])
    if(is_valid != None):
        return make_response(jsonify(is_valid), 400)

    # Save the image using the helper found in apihelpers
    filename = save_file(request.files['uploaded_image'])
    # If the filename is None something has gone wrong
    if(filename == None):
        return make_response(jsonify("Sorry, something has gone wrong"), 500)

    # Add row to DB like normal containing the information about the uploaded image
    results = run_procedure('CALL image_create(?,?)', [filename, request.form['description']])

    if(type(results) == list):
        return make_response(jsonify('Success'), 200)
    else:
        return make_response(jsonify(str(results)), 500)

@app.get('/api/image')
def get_image():
    # Make sure the image_id is sent
    is_valid = check_endpoint_info(request.args, ['image_id'])
    if(is_valid != None):
        return make_response(jsonify(is_valid), 400)

    # Get the image information from the DB
    results = run_procedure('CALL get_image(?)', [request.args.get('image_id')])
    # Make sure something came back from the DB that wasn't an error
    if(type(results) != list):
        return make_response(jsonify(str(results)), 500)
    elif(len(results) == 0):
        return make_response(jsonify("Invalid image id"), 400)

    # Use the built in flask function send_from_directory
    # First into the images folder, and then use my results from my DB interaction to get the name of the file
    return send_from_directory('images', results[0]['file_name'])


if(dbcreds.production_mode == True):
    print("Running in Production Mode")
    import bjoern # type: ignore
    bjoern.run(app, "0.0.0.0", 5000)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in Testing Mode")
    app.run(debug=True)