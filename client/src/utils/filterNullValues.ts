export const filterNullValuesFromObject = <T>(
  typedObj: T
): Record<string, any> => {
  const result = Object.keys(typedObj as Record<string, any>)
    .filter((key) => typedObj[key as keyof T] !== null)
    .reduce(
      (obj, key) => ({
        ...obj,
        [key]: typedObj[key as keyof T],
      }),
      {}
    );
  return result;
};
