import trackingImg from '@/assets/tracking_1.jpg';
import ctImg from '@/assets/ct_visualization.png';

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
    description: 'Upload a sequence of images taken over a period of time, and this ' +
                 'algorithm will stitch them together into a video.',
    imageUrl: 'none',
    to: '/timelapse',
    buttonText: 'Create your own',
    buttonIcon: 'av_timer',
  }, {
    title: 'Image Inpainting',
    description: 'This workflow allows you to erase areas of an image and have a neural ' +
                 'network intelligently fill in that area. Useful for touching up small ' +
                 'parts of your photos.',
    imageUrl: 'none',
    to: '/inpainting',
    buttonText: 'Try it out',
    buttonIcon: 'image',
  }],
  medical: [{
    title: 'CT Visualization',
    description: 'Use ParaView Glance to visualize a variety of medical and other data.',
    imageUrl: ctImg,
    to: '/glance',
    buttonText: 'Try it out',
    buttonIcon: 'keyboard_arrow_right',
  }, {
    title: 'Stroke Assessment',
    description: 'This algorithm will assess outcomes of stroke patients.',
    enabled: false,
    imageUrl: 'none',
  }, {
    title: 'Traumatic Brain Injury',
    description: 'Traumatic Brain Injury visualization workflow.',
    enabled: false,
    imageUrl: 'none',
  }],
};

export default demos;
