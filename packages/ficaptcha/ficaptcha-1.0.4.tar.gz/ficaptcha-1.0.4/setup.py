import setuptools

setuptools.setup(
	name="ficaptcha",
	version="1.0.4",
	author="Danil Kononyuk",
	author_email="me@0x7o.link",
	description="Simple captcha",
	long_description="""# fiCaptcha
Module for image-captcha generation

## Install
Build from source
```bash
git clone https://github.com/0x7o/fiCaptcha
cd fiCaptcha
pip install .
```

Python pip install
```bash
pip install ficaptcha
```
## Usage
# Image Captcha
Create a folder with images for captcha:
```bash
├── images
│   ├── toy
│       ├── toy1.png
│       ├── toy2.png
│       └── ...
│   └── fox
│       ├── fox1.png
│       ├── fox2.png
│       └── ...
```
Import the library and create a class
- ```size=(256, 256)``` - Captcha size in pixels
- ```image_dir="images"``` - Image folder for captcha
- ```background_color="white"``` - Background Color
- ```noise_bg=True``` - Whether or not to add noise to the background
- ```noise_im=True``` - Whether or not to add noise to the images
- ```rotate_im=True``` - Rotate images or not
- ```count_images=5``` - Number of images on the captcha
```python
from ficaptcha.image import Captcha

c = Captcha(size=(256, 256), image_dir="images", rotate_im=False)
```
Let's generate our captcha
```python
result = c.generate()
print(result)
```
```bash
{'class': 'toy', 'file': 'images/toy/toy5.png', 'position': (17, 139)}
```
""",
	long_description_content_type="text/markdown",
	url="https://github.com/0x7o/fiCaptcha",
	packages=setuptools.find_packages(),
	classifiers=[],
	python_requires='>=3.6',
)