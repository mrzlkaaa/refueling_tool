<template>
    <tr>
        <th v-for="data in datas" :key="data">
            {{data}}
        </th>
    </tr>
</template>
<script>
export default {
    name: "TableRowHeader",
    props: ["datas"],
}
</script>