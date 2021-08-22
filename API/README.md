## API for Delta Diagnose

<b> It is deployed on Heroku and can be accessed by sending a POST request on http://delta-diagnose-api.herokuapp.com/ </b> <br>
<b> Additionaly users can visit http://delta-diagnose-api.herokuapp.com/docs for documentation and trying it out. </b>

- Average response time 1.5 seconds.

### Parameters
It accepts JSON file containing Image URL.
Sample -
```
{
  "url" : "https://i.ibb.co/FBSztPS/0120.jpg"
}
```

### Response
It returns two things -
- class: covid/viral_pneumonia/normal
- class_probablity: How sure the model is that image belongs to the particular class
```
{
  "class":"viral",
  "class_probablity":99.93
}
```

### Installing and Running
- First Download the saved model from [here](https://drive.google.com/file/d/1PKPAZPQAYTVFsJcqNHNf4SvraDJb_LsU/view?usp=sharing) and paste it in saved_model folder.
- Run the following commands
```
pip install -r requirements.txt
uvicorn app:app
```
