

<script setup lang="ts">

import { onMounted, reactive, ref } from 'vue';
import { ArticleType } from '../types/article.type.ts'
import ArticleTag from './components/small/ArticleTag.small.vue'
import { fetchArticle, likeArticleService } from '../services/api.service.ts'

const state = reactive({
    loading: true,
    error: false
})


// Initialize the article object as empty
const article = ref<ArticleType>({
    id: 0,
    title: '',
    is_published: false,
    likes: 0,
    description: '',
    content: '',
    category: '',
    creation_date: '',
    tags: [],
});

const renderedHtml = ref(''); // Ref to store the rendered HTML


const likeArticle = () => {
    likeArticleService(article.value.id);
    article.value.likes++;
}


onMounted(() => {
    fetchArticle(state, renderedHtml, article);
});


</script>


<template>
    <section class="my-5 py-3">
        <div class="container">
            <div class="article-container mx-auto">
                <div v-if="state.loading" class="text-center">Fetching Article <span class="cursor">_</span></div>
                <div v-if="state.error" class="text-center">Error while fetching the article ...</div>
                <div class="pb-5 text-center">
                    <h1>{{ article.title }}</h1>
                    <div>
                        <small>{{ article.creation_date }}</small>
                    </div>
                    <div class="mt-3">
                        <span v-for="tag in article.tags" :key="tag">
                            <ArticleTag :tag="tag" />
                        </span>
                    </div>
                    <div class="mt-3 article-likes mx-auto">
                        <div @click="likeArticle"><i class="bi bi-heart icon"></i></div>
                        <div v-if="article.likes > 1">{{ article.likes }}</div>
                    </div>
                </div>
                <transition name="fade">
                    <div v-if="!state.loading" class="article-content" v-html="renderedHtml"></div>
                </transition>
            </div>
        </div>
    </section>
</template>



<style scoped>
.article-container {
    width: 75%;
}

.article-likes {
    width: 10%;
}

.article-likes i {
    font-size: larger;
}

.article-likes i:hover, .article-likes div:hover {
    cursor: pointer;
    color: var(--primary);
}

@media (max-width: 768px) {
    .article-container {
        width: 90%;
    }
}
</style>