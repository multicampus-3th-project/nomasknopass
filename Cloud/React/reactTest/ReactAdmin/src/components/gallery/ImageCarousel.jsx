import React from "react";
import {
  Carousel,
  CarouselItem,
  CarouselControl,
  CarouselIndicators,
  CarouselCaption
} from "reactstrap";

class ImageCarousel extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      activeIndex: 0,
      animating: false
    };
  }
  componentDidMount() {
    this.setState({ activeIndex: this.props.currentIndex });
  }

  next = () => {
    const { animating, activeIndex } = this.state;
    const { images } = this.props;
    if (animating) return;
    const nextIndex = activeIndex === images.length - 1 ? 0 : activeIndex + 1;
    this.setState({ activeIndex: nextIndex });
  };

  previous = () => {
    const { animating, activeIndex } = this.state;
    const { images } = this.props;
    if (animating) return;
    const nextIndex = activeIndex === 0 ? images.length - 1 : activeIndex - 1;
    this.setState({ activeIndex: nextIndex });
  };

  goToIndex = newIndex => {
    const { animating } = this.state;
    if (animating) return;
    this.setState({ activeIndex: newIndex });
  };

  setAnimating = value => {
    this.setState({
      animating: value
    });
  };

  render() {
    const { images } = this.props;
    const { activeIndex } = this.state;
    const slides = images.map(image => {
      return (
        <CarouselItem
          onExiting={() => this.setAnimating(true)}
          onExited={() => this.setAnimating(false)}
          key={image.id}
        >
          <div className="d-flex justify-content-center">
            <img src={image.url} alt={image.title} className="img-fluid" />
          </div>
        </CarouselItem>
      );
    });

    return (
      <Carousel
        activeIndex={activeIndex}
        next={this.next}
        previous={this.previous}
      >
        <CarouselIndicators
          items={images}
          activeIndex={activeIndex}
          onClickHandler={this.goToIndex}
        />
        {slides}
        <CarouselControl
          direction="prev"
          directionText="Previous"
          onClickHandler={this.previous}
        />
        <CarouselControl
          direction="next"
          directionText="Next"
          onClickHandler={this.next}
        />
      </Carousel>
    );
  }
}

export default ImageCarousel;
