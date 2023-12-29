import axios from "axios";
import { Ref } from 'vue'
import { ArticleInGridType, ArticleType } from '../types/article.type.ts'
import MarkdownIt from 'markdown-it';
import mdHighlight from 'markdown-it-highlightjs';
import { useRoute } from 'vue-router';


interface State {
  loading: boolean,
  error: boolean
}

const BASE_URL = import.meta.env.VITE_API_URL;

export const fetchArticles = async (state: State, articles: Ref<ArticleInGridType[]>) => {
  try {

    const data = await axios.get(`${BASE_URL}/articles/`, {
      headers: {
        'Content-Type': 'application/json',
      }
    });
    if (data === null) {
      state.loading = false
      state.error = true
      throw new Error("No data returned from API.")
    }
    else {
      articles.value = data.data;
      state.loading = false
    }


  } catch (err: any) {
    state.loading = false
    state.error = true
    throw new Error(err)
  }
}



export const fetchTagsList = async () => {

  try {
    const response = await axios.get(`${BASE_URL}/tags/`, {
      headers: {
        'Content-Type': 'application/json',
      }
    })

    return response.data;

  } catch (error: any) {
    return null;
  }
};



export const fetchCategoryList = async () => {

  try {
    const response = await axios.get(`${BASE_URL}/categories/`, {
      headers: {
        'Content-Type': 'application/json',
      }
    })

    return response.data;

  } catch (error: any) {
    return null;
  }
};


export const fetchArticle = async (state: State, renderedHtml: Ref<string>, article: Ref<ArticleType>) => {
  try {

    const route = useRoute();

    const id = route.params.id.toString();
    const response = await axios.get(`${BASE_URL}/article/${id}`, {
      headers: {
        'Content-Type': 'application/json',
      }

    });

    if (response === null) {

      state.loading = false
      state.error = true
      throw new Error("No data returned from API.")
    }
    else {
      article.value = response.data;
      const md = new MarkdownIt().use(mdHighlight);
      renderedHtml.value = md.render(article.value.content);
      state.loading = false
    }


  } catch (err: any) {
    state.loading = false
    state.error = true
    throw new Error('Could not get article.')
  }
}

