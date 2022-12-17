

export class Certificate {
    constructor(c: Partial<Certificate>) {
        Object.assign(this, c)
    }
    subject: string
    alt_names: string[]
}
