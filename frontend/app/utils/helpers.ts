export function toCarouselImage(image: PortfolioImage) {
  return {
    url: image.imageUrl,
    name: image.artName,
  };
}
