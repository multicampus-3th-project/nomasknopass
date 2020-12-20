import React from 'react';
import Carousel, { Modal, ModalGateway } from 'react-images';

const images = [{ src: 'https://kf99-cctv-image.s3.ap-northeast-2.amazonaws.com/cctv-image.jpg' }, { src: 'https://kf99-cctv-image.s3.ap-northeast-2.amazonaws.com/cctv-image.jpg' }];

class Gallery extends React.Component {
  state = { modalIsOpen: true }
  toggleModal = () => {
    this.setState(state => ({ modalIsOpen: !state.modalIsOpen }));
  }
  render() {
    const { modalIsOpen } = this.state;

    return (
      <ModalGateway>
        {modalIsOpen ? (
          <Modal onClose={this.toggleModal}>
            <Carousel views={images} />
          </Modal>
        ) : null}
      </ModalGateway>
    );
  }
}
export default Gallery;