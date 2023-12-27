import axios from 'axios';


const getArticlesList = async () => {
  const response = await axios.get('http://127.0.0.1:8000/api/v1/articles/', {
    headers: {
      'Content-Type': 'application/json',
    }
  });
  return response.data;
}


const getSingleArticle = async (article_id: string) => {
  const response = await axios.get(`http://127.0.0.1:8000/api/v1/article/${article_id}`, {
    headers: {
      'Content-Type': 'application/json',
    }
  });
  return response.data;
}


export default { getArticlesList, getSingleArticle };
