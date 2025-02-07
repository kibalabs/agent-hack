/* eslint-disable */
const { Tag, MetaTag } = require('@kibalabs/build/scripts/plugins/injectSeoPlugin.js');

const title = 'Yield Seeker';
const description = 'The Best AI Agent for Maximizing Crypto Yields';
const url = 'https://app.yieldseeker.xyz'
const imageUrl = `${url}/assets/banner.png`;

const seoTags = [
  new MetaTag('description', description),
  new Tag('meta', {property: 'og:title', content: title}),
  new Tag('meta', {property: 'og:description', content: description}),
  new Tag('meta', {property: 'og:url', content: url}),
  new Tag('meta', {property: 'og:image', content: imageUrl}),
  new MetaTag('twitter:card', 'summary_large_image'),
  new MetaTag('twitter:site', '@tokenpagexyz'),
  new Tag('link', {rel: 'canonical', href: url}),
  new Tag('link', {rel: 'icon', type: 'image/png', href: '/assets/icon.png'}),
];

module.exports = (config) => {
  config.seoTags = seoTags;
  config.title = title;
  config.analyzeBundle = false;
  return config;
};
