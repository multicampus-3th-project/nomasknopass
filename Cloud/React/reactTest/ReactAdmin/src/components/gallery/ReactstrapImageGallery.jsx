import React from "react";
import {
    Modal,
    ModalHeader,
    ModalFooter,
    ModalBody,
    Col,
    Row,
    Container,
    Card,
    CardImgOverlay,
    CardImg,
    Button
} from "reactstrap";

import ImageCarousel from "./ImageCarousel";

class ReactstrapImageGallery extends React.Component {
    contructor(props) {
        this.state = {
            isModalOpen: false, // state for the modal popup
            images: [], // images array we receive from the parent
            imagesToShow: 0, // limit 
            currentIndex: 0 // used for the carousel
        }
    }
    static getDerivedStateFromProps(props, state) {
        const { images, limit } = props;
        const imagesToShow = props.hasOwnProperty("limit") ? limit : 6;
        return { images, imagesToShow };
    }

    // for toggling the modal state
    toggleModal = () => {
        this.setState({
            isModalOpen: !this.state.isModalOpen
        })
    }

    // used to set the current index of the carousel
    showModalImage = imageId => {
        this.toggleModal();
        this.setState({
            currentIndex: imageId
        })
    }


    render() {
        const { isModalOpen, images, imagesToShow, currentIndex } = this.state;
        const tempImagesArray = images.slice(0, imagesToShow); //temporary array
        const hasMore = images.length !== 0 ? images.length - imagesToShow : 0;

        return (
            <>
            <Row>
                <Col md={{ size: 10, offset: 1 }}>
                    <h5 className="text-center my-3"></h5>
                    <Row>
                        {tempImagesArray.map((image, index) => (
                            <Col
                                md="4"
                                key={index}
                                onClick={() => this.showModalImage(index)}
                            >
                                <Card className="image-card">
                                    <CardImg src={image.url} />
                                    {hasMore !== 0 && index === imagesToShow - 1 ? (
                                        <CardImgOverlay className="overlay">
                                            <h2 className="mb-0">{hasMore}</h2>
                                            <small> More </small>
                                        </CardImgOverlay>
                                    ) : null}
                                </Card>
                            </Col>
                        ))}
                    </Row>
                </Col>
            </Row>

            <Modal
                className="modal-xl"
                isOpen={isModalOpen}
                toggle={this.toggleModal}
            >
                <ModalHeader>CCTV 모니터링</ModalHeader>
                <ModalBody>
                    <Row>
                        <Col md="12">
                            <ImageCarousel images={images} currentIndex={currentIndex} />
                        </Col>
                    </Row>
                </ModalBody>
            </Modal>
</>

        );
    }
}

export default ReactstrapImageGallery;