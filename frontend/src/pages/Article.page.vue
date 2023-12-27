

<script setup lang="ts">

import { onMounted, reactive, ref } from 'vue';
import MarkdownIt from 'markdown-it';
import mdHighlight from 'markdown-it-highlightjs';
import api from '../services/api.ts';
import { ArticleType } from '../types/article.type.ts'
import { useRoute } from 'vue-router';
import ArticleTag from './components/small/ArticleTag.small.vue'


const route = useRoute();

onMounted(async () => {
    const id = route.params.id.toString();
    const response = await api.getSingleArticle(id);
    article.value = response;

    const md = new MarkdownIt().use(mdHighlight);
    renderedHtml.value = md.render(article.value.content);
    state.loading = false
})

// Initialize the article object as empty
const article = ref<ArticleType>({
    id: 0,
    title: '',
    description: '',
    content: '',
    creation_date: '',
    tags: [],
});

const state = reactive({
    loading: true,
})

const renderedHtml = ref(''); // Ref to store the rendered HTML

</script>


<template>
    <section class="my-5 py-3">
        <div class="container">
            <div class="article-container mx-auto">
                <div v-if="state.loading" class="text-center">Fetching Article ...</div>
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

@media (max-width: 768px) {
    .article-container {
        width: 90%;
    }
}
</style>