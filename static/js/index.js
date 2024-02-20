function handleTopicChange() {
    const selectElement = document.getElementById('debate-topics');
    const topicId = selectElement.value;
    if (!topicId) return;

    fetch(`/api/topic-info?topic_id=${topicId}`)
        .then(response => response.json())
        .then(data => {
            document.querySelector('h1').textContent = data.page_title;
            document.querySelector('p').textContent = data.welcome_message;
        })
        .catch(error => console.error("Error:", error));
}