import axios from "axios";
import { Ref } from 'vue'
import { ArticleInGridType } from '../types/article.type.ts'

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




