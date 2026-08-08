export type PortfolioImage = {
  id: string;
  artName: string;
  imageUrl: string;
  uploadId: string;
  userId: string;
  createdAt: string;
  updatedAt: string;
};

export type PublicPortfolio = {
  id: string;
  userId: string;
  description: string;
  commissionSlots: number;
  createdAt: string;
  updatedAt: string;
  images: PortfolioImage[];
};

export type PublicPortfolioPage = {
  items: PublicPortfolio[];
  page: number;
  pageSize: number;
  total: number;
  hasNext: boolean;
};

export type CarouselImage = {
  url: string;
  name: string;
};

export type PortfolioSettings = {
  id: string;
  userId: string;
  description: string;
  isPublic: boolean;
  commissionSlots: number;
  createdAt: string;
  updatedAt: string;
};

export type MenuItem = {
  label?: string;
  to?: string;
  icon?: string;
  items?: MenuItem[];
  command?: () => void;
};
