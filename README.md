<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!-- PROJECT LOGO -->
<br />
<div align="center">

<h3 align="center">img-edit</h3>

  <p align="center">
    A small HTTP API for cropping and rotating images, built with FastAPI and OpenCV.
    <br />
    <a href="#usage"><strong>See usage examples »</strong></a>
    <br />
    <br />
    <a href="https://github.com/K0Stek122/img-edit/issues/new?labels=bug">Report Bug</a>
    &middot;
    <a href="https://github.com/K0Stek122/img-edit/issues/new?labels=enhancement">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#endpoints">Endpoints</a></li>
        <li><a href="#rotate-an-image">Rotate an image</a></li>
        <li><a href="#crop-an-image">Crop an image</a></li>
        <li><a href="#errors">Errors</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

img-edit is a lightweight image-editing service. You upload an image with a multipart form request, and the API returns the edited image as a PNG.

Features:
* **Crop** an image to a rectangular region
* **Rotate** an image by 90° clockwise, 180° or 90° counterclockwise
* Accepts any format OpenCV can decode (JPEG, PNG, WebP, BMP, TIFF, …)
* Keeps transparency: alpha channels in PNGs survive the edit
* Validates input and returns clear error messages for bad coordinates, unknown rotations or files that aren't images
* Interactive API docs out of the box at `/docs`

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][Python.org]][Python-url]
* [![FastAPI][FastAPI.com]][FastAPI-url]
* [![OpenCV][OpenCV.org]][OpenCV-url]
* [![NumPy][NumPy.org]][NumPy-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Follow these steps to run the API locally.

### Prerequisites

* Python 3.10 or newer
  ```sh
  python3 --version
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/K0Stek122/img-edit.git
   cd img-edit
   ```
2. Create and activate a virtual environment (optional, but recommended)
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install the dependencies
   ```sh
   pip install -r requirements.txt
   ```
4. Start the development server
   ```sh
   fastapi dev main.py
   ```
   The API is now running at `http://localhost:8000`. For production, use `fastapi run main.py` instead.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

All editing endpoints take a `multipart/form-data` request. The image goes in a field named **`file`**, and the result comes back as raw PNG bytes (`Content-Type: image/png`). Uploads are limited to 20 MB.

### Endpoints

| Method | Path            | Form fields                                          | Returns           |
|--------|-----------------|------------------------------------------------------|-------------------|
| GET    | `/health-check` | none                                                 | `{"message": "Running"}` |
| POST   | `/rotate`       | `file`, `rotation`                                   | PNG image         |
| POST   | `/crop`         | `file`, `x_start`, `x_end`, `y_start`, `y_end`       | PNG image         |

### Rotate an image

`rotation` must be one of:

| Value | Rotation             |
|-------|----------------------|
| `0`   | 90° clockwise        |
| `1`   | 180°                 |
| `2`   | 90° counterclockwise |

```sh
curl -X POST http://localhost:8000/rotate \
  -F "file=@photo.jpg" \
  -F "rotation=0" \
  -o rotated.png
```

### Crop an image

Coordinates are in pixels, measured from the top-left corner. The start is inclusive and the end is exclusive, and they must satisfy `0 <= start < end <= image size`.

```sh
curl -X POST http://localhost:8000/crop \
  -F "file=@photo.jpg" \
  -F "x_start=0" -F "x_end=200" \
  -F "y_start=0" -F "y_end=200" \
  -o cropped.png
```

### Errors

Errors are returned as JSON in the form `{"detail": "..."}`.

| Status | Cause |
|--------|-------|
| `400`  | The file couldn't be decoded as an image, or the crop region is outside the image |
| `413`  | The upload is larger than 20 MB |
| `422`  | A required field is missing, has the wrong type, or `rotation` isn't 0, 1 or 2 |

> **Tip:** while testing with curl, use `-i` instead of `-o` to see the status code and error message.

_For interactive documentation where you can try every endpoint from the browser, open [http://localhost:8000/docs](http://localhost:8000/docs) while the server is running._

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Crop
- [x] Rotate by 90° steps
- [ ] Resize / scale
- [ ] Rotate by an arbitrary angle
- [ ] Flip horizontally / vertically
- [ ] Choose the output format (JPEG, WebP, …)
- [ ] Tests

See the [open issues](https://github.com/K0Stek122/img-edit/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/K0Stek122/img-edit/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=K0Stek122/img-edit" alt="contrib.rocks image" />
</a>



<!-- LICENSE -->
## License

This project doesn't have a license yet. Until one is added, all rights are reserved by the author.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

K0Stek122 - [github.com/K0Stek122](https://github.com/K0Stek122)

Project Link: [https://github.com/K0Stek122/img-edit](https://github.com/K0Stek122/img-edit)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Best-README-Template](https://github.com/othneildrew/Best-README-Template)
* [FastAPI documentation](https://fastapi.tiangolo.com/)
* [OpenCV documentation](https://docs.opencv.org/)
* [Shields.io](https://shields.io/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/K0Stek122/img-edit.svg?style=for-the-badge
[contributors-url]: https://github.com/K0Stek122/img-edit/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/K0Stek122/img-edit.svg?style=for-the-badge
[forks-url]: https://github.com/K0Stek122/img-edit/network/members
[stars-shield]: https://img.shields.io/github/stars/K0Stek122/img-edit.svg?style=for-the-badge
[stars-url]: https://github.com/K0Stek122/img-edit/stargazers
[issues-shield]: https://img.shields.io/github/issues/K0Stek122/img-edit.svg?style=for-the-badge
[issues-url]: https://github.com/K0Stek122/img-edit/issues
[Python.org]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[FastAPI.com]: https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white
[FastAPI-url]: https://fastapi.tiangolo.com/
[OpenCV.org]: https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white
[OpenCV-url]: https://opencv.org/
[NumPy.org]: https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white
[NumPy-url]: https://numpy.org/
