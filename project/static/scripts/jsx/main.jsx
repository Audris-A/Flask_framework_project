var slideIndex = 1;

function showSlides(n){
    var i;
    var slides = document.getElementsByClassName("mySlides");
    var dots = document.getElementsByClassName("dot");
    if (n > slides.length) {slideIndex = 1}
    if (n < 1) {slideIndex = slides.length}
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex-1].style.display = "block";
    dots[slideIndex-1].className += " active";
}

class Imageslider extends React.Component {
  componentDidMount() {

    var i;
    var n = slideIndex;
    var slides = document.getElementsByClassName("mySlides");
    if (n > slides.length) {slideIndex = 1}
    if (n < 1) {slideIndex = slides.length}
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    slides[slideIndex-1].style.display = "block";
  }

  render() {
      var imageLink = "../../static/images/image";
      var imageArray = [];

      var imageCount = 10;

      for (var i = 1 ; i < imageCount + 1; i++) {
        var imageObjLink = imageLink + String(i) + ".jpg";
        imageArray.push(imageObjLink);
      }

      const imagestyle = {
          width: "100%",
          maxWidth: "100%",
          height: "auto",
          fontFamily: "Arial"
      };

      const imageList = imageArray.map((pathToImage, index) =>
        <div key={pathToImage} className="mySlides slideShowImagefade">
          <div className="numbertext">{index + 1} / {imageCount}</div>
          <img src={pathToImage} style={imagestyle}/>
        </div>
      );

    return imageList;
  }
};

ReactDOM.render(
  <Imageslider />,
  document.getElementById('imageSlider')
);

class Dotcomponent extends React.Component {
  componentDidMount() {
    var i;
    var dots = document.getElementsByClassName("dot");
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    dots[slideIndex-1].className += " active";
  }

  currentSlide(n) {
    showSlides(slideIndex = n);
  }

  render() {
      var numArray = [];

      for (var i = 1 ; i < 11; i++) {
        numArray.push(i);
      }

      const dotList = numArray.map((iter) =>
        <span key={iter} className="dot" onClick={() => this.currentSlide(iter)}></span>
      );

      return dotList;
  }
};

ReactDOM.render(
  <Dotcomponent />,
  document.getElementById('dotObject')
);

class Sliderbuttons extends React.Component {
  plusSlides(n) {
    showSlides(slideIndex += n);
  }

  render() {
      const buttons = (
        <div>
          <a className="prev" onClick={() => this.plusSlides(-1)}>&#10094;</a>
          <a className="next" onClick={() => this.plusSlides(1)}>&#10095;</a>
        </div>
      );

    return buttons;
  }
};

ReactDOM.render(
  <Sliderbuttons />,
  document.getElementById('sliderButtons')
);