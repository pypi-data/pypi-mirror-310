import {Image, ImageObjectContainer} from "./ImageObject.style.tsx";
import {Skeleton} from "@mui/material";
import {useEffect, useState} from "react";

export default function ImageObject(props: { bucketName: string, objectKey: string }) {
    const {bucketName, objectKey} = props;
    const [loading, setLoading] = useState(true);
    const [imageBlobUrl, setImageBlobUrl] = useState('');

    useEffect(() => {
        const loadImage = async () => {
            const url = `/api/v1/buckets/${bucketName}/object?key=${encodeURIComponent(objectKey)}`;
            const res = await fetch(url);
            const blob = await res.blob();
            setImageBlobUrl(URL.createObjectURL(blob));
            setLoading(false);
        };
        loadImage();
    }, []);

    return (
        <ImageObjectContainer>
            {loading && <Skeleton variant="rectangular" width={180} height={180}/>}
            {!loading && <Image src={imageBlobUrl} alt={objectKey}/>}
        </ImageObjectContainer>
    );
}