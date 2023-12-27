import axios from 'axios';


const getArticlesList = async () => {

  try {
    const response = await axios.get('http://127.0.0.1:8000/api/v1/articles/', {
      headers: {
        'Content-Type': 'application/json',
      }
    })

    return response.data;

  } catch (error: any) {
    return null;
  }

};

const getSingleArticle = async (article_id: string) => {

  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/v1/article/${article_id}`, {
      headers: {
        'Content-Type': 'application/json',
      }

    });
    return response.data;

  } catch {
    return (error: any) => {

      console.log(error);
      return null;
    };
  }

};




export default { getArticlesList, getSingleArticle };
