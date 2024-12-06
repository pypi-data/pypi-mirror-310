export function parseBucketName(path: string | undefined): string | undefined {
    return path?.split('/')[0];
}

export function parseObjectKey(path: string | undefined): string | undefined {
    const slashIndex = path?.indexOf('/');
    if (slashIndex && slashIndex > 0) {
        return path?.substring(path?.indexOf('/') + 1);
    } else {
        return undefined;
    }
}