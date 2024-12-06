import {useParams} from "react-router-dom";
import {useEffect, useState} from "react";
import ImageObject from "./ImageObject.tsx";
import {parseBucketName, parseObjectKey} from "../utils.ts";

export default function ObjectGrid() {
    const {'*': path} = useParams();
    const bucketName = parseBucketName(path);
    const objectKey = parseObjectKey(path);
    const [objectKeys, setObjectKeys] = useState<string[]>([]);

    useEffect(() => {
        if (bucketName) {
            const loadBuckets = async () => {
                let url = `/api/v1/buckets/${bucketName}/objects`;
                if (objectKey) {
                    url += `?prefix=${objectKey}/`;
                }
                const res = await fetch(url);
                const json = await res.json();
                setObjectKeys(json.objects.filter((o: string) => isImageKey(o)));
            };
            loadBuckets();
        }
    }, [bucketName, objectKey]);

    const isImageKey = (key: string) => {
        return key.toLowerCase().endsWith('.jpg') || key.toLowerCase().endsWith('.jpeg') || key.toLowerCase().endsWith('.png');
    }

    if (bucketName) {
        return (
            <div style={{display: 'flex', flexWrap: 'wrap'}}>
                {objectKeys.map(k => <ImageObject key={k} bucketName={bucketName} objectKey={k}/>)}
            </div>
        );
    }

}