# security_system
Modular Project in progress.
People detector in a designated area, focused on home or business entrances, using a trained CNN model and OpenCV
The main menu show 3 options:

New Area:

-Create a new area to detect movement based on the selected camera.

-Save the coordinates and an image of the designated area.

Settings:

-Configure the camera.

-The camera can be an IP camera, a webcam, or a physical camera (0/1 for local devices).

Start:

-Start the detection process, focusing on the specified coordinates.

-When a change is detected for more than 3 seconds in at least 10% of the designated area:

-Take 5 captures and evaluate them using the CNN model.

-Upload the images to the server.

-If 3 or more images are classified as "human," send an alert message via SMPP with the URL of the new detection.

