const sleep = (ms=2000) => new Promise(res => setTimeout(res, ms));

export { sleep };