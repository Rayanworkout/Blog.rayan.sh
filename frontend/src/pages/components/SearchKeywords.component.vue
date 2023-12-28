
<script setup lang="ts">
import axios from 'axios';
import ArticleTag from './small/ArticleTag.small.vue'
import { onMounted, ref } from 'vue';

type tag = string;

const tags = ref<tag[][]>([]);

// Split tags by groups of 4 to display 4 per row
const splitTags = (tags: string[]) => {
    const result: string[][] = [];
    for (let i = 0; i < tags.length; i += 4) {
        result.push(tags.slice(i, i + 4));
    }
    return result;
};


const getTagsList = async () => {

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

onMounted(async () => {
    const fetchedTags = await getTagsList();
    tags.value = splitTags(fetchedTags);

});

</script>


<template>
    <div class="container">
        <div class="text-center">
            <input type="text" placeholder="Search">
            <ul v-for="tagList in tags" :key="tagList[0]"
                class="list-inline list-unstyled d-flex justify-content-center pt-3 tag-list">
                <div v-for="tag in tagList">
                    <ArticleTag :tag="tag" class="tag" />
                </div>

            </ul>
        </div>
    </div>
</template>


<style scoped>
input {
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 5px;
    width: 15%;
    max-width: 500px;
}

.tag-list {
    margin: 0;
    padding: 0;

}

.tag {
    font-size: 0.9em;
}

@media (max-width: 768px) {
    input {
        width: 50%;
    }
    .tag {
        font-size: 0.65em;
    }
}

</style>