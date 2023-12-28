import axios from "axios";
import { Ref } from 'vue'
import { ArticleInGridType } from '../types/article.type.ts'

interface State {
  loading: boolean,
  error: boolean
}


export const fetchArticles = async (state: State, articles: Ref<ArticleInGridType[]>) => {
  try {
    const data = await axios.get('http://127.0.0.1:8000/api/v1/articles/', {
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
    const response = await axios.get('http://127.0.0.1:8000/api/v1/tags/', {
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
    const response = await axios.get('http://127.0.0.1:8000/api/v1/categories/', {
      headers: {
        'Content-Type': 'application/json',
      }
    })

    return response.data;

  } catch (error: any) {
    return null;
  }
};

