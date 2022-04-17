<template>
    <tr >
        <td v-for="data in content" :key="data">
            {{data}}
        </td>
    </tr>
</template>
<script>
export default {
    name: "TableRowBody",
    inject:["content"]
}
</script>