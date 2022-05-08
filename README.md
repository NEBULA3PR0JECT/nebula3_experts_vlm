# nebula3_experts_vlm
## Base module for all experts

## HOW TO USE THIS REPO from VSCODE:
1. `git clone https://github.com/NEBULA3PR0JECT/nebula3_experts_vlm.git --recursive`

## HOW TO USE THIS REPO with DOCKER:

**First, clone this repo:**
1. `git clone https://github.com/NEBULA3PR0JECT/nebula3_experts_vlm.git --recursive`

**For GPU usage (recommended):**

2. `cd Docker && cd microservice-gpu`

**For CPU usage (not recommended, unless you're 100% sure you don't need gpu):**

2. `cd Docker && cd microservice-cpu`

**Build the docker: (For e.g. with GPU)**

3. `docker build -t microservice-vlm-gpu .`

*Note:* You can change `microservice-expert` to your desired image name.

**Run the docker (with GPU):**

4. `docker run -it -p 8088:8088 --gpus all microservice-vlm-gpu:latest`

**Run the docker (with CPU):**

4. `docker run -it -p 8088:8088 microservice-vlm-cpu:latest`

**How to use VLM and predict on text:**

`curl http://localhost:8088/predict-on-txt/{your-desired-text}`

For e.g., if I want to encode the string `nebula` it should be

`curl http://localhost:8088/predict-on-txt/nebula`

**How to use VLM and predict on video:**

`curl http://localhost:8088/predict-on-video/{movie-id}/{scene_element}`

For e.g., if I want to encode the movie `114208777`, and scene_element `0`, it should be:

`curl http://localhost:8088/predict-on-video/114208777/0`

*Note*: For more info. on the available functionality you can always check `http://localhost:8088/docs`
