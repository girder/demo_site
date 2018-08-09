import trackingImg from '@/assets/tracking_1.jpg';
import ctImg from '@/assets/ct_visualization.png';
import inpaintingImg from '@/assets/inpainting.png';

const demos = {
  vision: [{
    title: 'Tracking',
    description: 'This video demonstrates various tracking capabilities developed by our ' +
                 'computer vision team.',
    imageUrl: trackingImg,
    href: 'https://vimeo.com/90767973',
    buttonText: 'Watch',
    buttonIcon: 'play_circle_filled',
  }, {
    title: 'Timelapse Video Creation',
    description: 'Upload a sequence of images taken over a period of time, and our ' +
                 'algorithm will stitch them together into a video.',
    imageUrl: 'none',
    to: '/timelapse',
    buttonText: 'Create your own',
    buttonIcon: 'av_timer',
  }, {
    title: 'Image Inpainting',
    description: 'This workflow allows you to erase areas of an image and have a neural ' +
                 'network intelligently fill in that area.',
    imageUrl: inpaintingImg,
    to: '/inpainting',
    buttonText: 'Try it out',
    buttonIcon: 'image',
  }],
  medical: [{
    title: 'Medical Data Visualization',
    description: 'Use ParaView Glance to visualize a variety of 3D medical images and ' +
                 'data in your browser.',
    imageUrl: ctImg,
    to: '/glance',
    buttonText: 'Try it out',
    buttonIcon: 'keyboard_arrow_right',
  }, {
    title: 'Stroke Assessment',
    description: 'Analyze intracranial vasculature in acute stroke CT scans to identify the ' +
                 'presence of collateral vessels that support recovery.',
    enabled: false,
    imageUrl: 'none',
  }, {
    title: 'Tumors & TBI',
    description: 'Upload a T1 MRI scan and have our system estimate the brain\'s appearance ' +
                 'prior to injury and the changes induced by the injury.',
    enabled: false,
    imageUrl: 'none',
  }],
};

export default demos;
