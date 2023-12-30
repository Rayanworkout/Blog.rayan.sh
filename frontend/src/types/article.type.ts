


export type ArticleInGridType = {
    id: number;
    title: string;
    description: string;
    category: string;
    tags: string[];
    creation_date: string;
}

export type ArticleType = {
    id: number;
    title: string;
    description: string;
    is_published: boolean;
    likes: number;
    category: string;
    tags: string[];
    creation_date: string;
    content: string;
}
