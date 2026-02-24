export async function submitForm(payload) {
    // POST /submit
    return new Promise(resolve => {
        setTimeout(() => {
            resolve({ jobId: 'job-' + Date.now() })
        }, 500)
    })
}

export async function checkJobStatus(jobId) {
    // GET /status/:jobId
    return new Promise(resolve => {
        setTimeout(() => {
            const done = Math.random() > 0.7
            resolve({
                status: done ? 'complete' : 'processing',
                result: done ? { message: 'Job finished successfully' } : null
            })
        }, 500)
    })
}
