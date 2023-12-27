
<script setup lang="ts">
import { ArticleInGridType } from '../../types/article.type.ts'
import ArticleTag from './small/ArticleTag.small.vue'

defineProps<{ article: ArticleInGridType }>()

</script>


<template>
    
    <div class="article mx-auto">
        <div class="row mb-2 border-bottom">
            <div class="col-md-6">
                <router-link :to="{ name: 'Article', params: { id: article.id } }" class="article-link">
                    <h4>{{ article.title }}</h4>

                    <div class="mb-2 date">
                        <small>{{ article.creation_date }}</small>
                    </div>
                </router-link>
            </div>

            <div class="col-md-6 text-center pb-3 d-flex justify-content-center align-items-center">
                <span v-for="tag in article.tags" :key="tag">
                    <ArticleTag :tag="tag" />
                </span>
            </div>
        </div>
        <router-link :to="{ name: 'Article', params: { id: article.id } }" class="article-link">
            <p>{{ article.description }}</p>
        </router-link>

    </div>
</template>
  

<style scoped>
.article {
    border: 1px solid #ccc;
    border-radius: 7px;
    padding: 1rem;
    margin-bottom: 1rem;
    transition: all 0.3s ease-in-out;
    width: 60%;
    overflow: hidden;
}

h4 {
    transition: all 0.3s ease-in-out;
}

h4:hover {
    color: var(--primary);
    width: fit-content;
    cursor: pointer;
}

.article:hover {
    transform: scale(1.02);
    border-color: var(--primary);
    cursor: pointer;
}

.article-link {
    text-decoration: none;
    color: inherit;
}

.arrow:hover {
    color: var(--primary);
}


@media (max-width: 768px) {
    .article {
        width: 100%;
    }

    h4,
    .date {
        text-align: center;
    }
}
</style>