import trackingImg from '@/assets/tracking_1.jpg';
import ctImg from '@/assets/ct_visualization.png';
import inpaintingImg from '@/assets/inpainting.jpg';
import recognitionImg from '@/assets/recognition.png';
import surgicalImg from '@/assets/surgical.jpg';
import strokeImg from '@/assets/Stroke.jpg';
import tbiImg from '@/assets/TBI.jpg';

const VIDEO_ICON = 'play_circle_filled';

const demos = {
  vision: [{
    title: 'Tracking',
    description: 'This video demonstrates various tracking capabilities developed by our ' +
                 'computer vision team.',
    imageUrl: trackingImg,
    video: {
      src: 'https://player.vimeo.com/video/90767973',
      width: 640,
      height: 360,
    },
    href: 'https://vimeo.com/90767973',
    buttonText: 'Watch',
    buttonIcon: VIDEO_ICON,
  }, {
    title: 'Activity Recognition',
    description: 'Complex activity recognition using Granger Constrained DBN (GDBN) in sports ' +
                 'and surveillance video.',
    imageUrl: recognitionImg,
    video: {
      src: 'https://player.vimeo.com/video/97850118',
      width: 640,
      height: 480,
    },
    href: 'https://vimeo.com/97850118',
    buttonText: 'Watch',
    buttonIcon: VIDEO_ICON,
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
    title: 'Surgical Simulation',
    description: 'Using computer-tracked laparoscopic hardware and an augmented reality display,' +
                 ' surgical simulation can reduce surgeon training time, costs, and risks.',
    imageUrl: surgicalImg,
    video: {
      src: 'https://player.vimeo.com/video/191839695',
      width: 640,
      height: 360,
    },
    href: 'https://vimeo.com/191839695',
    buttonText: 'Watch',
    buttonIcon: VIDEO_ICON,
  }, {
    title: 'Stroke Assessment',
    description: 'Analyze intracranial vasculature in acute stroke CT scans to identify the ' +
                 'presence of collateral vessels that support recovery.',
    to: '/stroke_ct',
    buttonText: 'Try it out',
    imageUrl: strokeImg,
  }, {
    title: 'Tumors & Traumatic Brain Injury',
    description: 'Upload a T1 MRI scan and have our system estimate the brain\'s appearance ' +
                 'prior to injury and the changes induced by the injury.',
    enabled: false,
    imageUrl: tbiImg,
  }],
  cloud: [{
    title: 'Timelapse Video Creation',
    description: 'Upload a sequence of images taken over a period of time, and our ' +
                 'algorithm will stitch them together into a video.',
    enabled: false,
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
};

export default demos;
