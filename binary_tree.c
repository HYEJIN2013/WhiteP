#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

#define MAXWORD 100
#define MIN 0
#define MAX 1

typedef struct tnode {
    char *word;
    struct tnode *left;
    struct tnode *right;
} tnode_t;


void freenode(tnode_t *p);
void alldeletenode(tnode_t *);

tnode_t * addnode(tnode_t *, char *);
tnode_t * deletenode(tnode_t *, char *);

tnode_t * getreplace(tnode_t *, tnode_t **);
tnode_t *getnode(tnode_t *, tnode_t **, const char *);

void treeprint(tnode_t *);
int getword(char *, int);
tnode_t *talloc(void);
char * strdup(char *);


int main(int argc, char *argv[])
{
    tnode_t *root;
    char word[MAXWORD] = {0};
    char *ptr = word;
    root = NULL;

    fprintf(stdout, "# Input tree nodes ######\n");
    getword(word, MAXWORD);

    ptr = strtok(word, " ");
    if (ptr) { 
        root = addnode(root, ptr);
    }

    while(NULL != (ptr = strtok(NULL, " "))) { 
        root = addnode(root, ptr);
    }

    fprintf(stdout, "# currnt, tree print ######\n");
    treeprint(root);

    fprintf(stdout, "\n# Input delete node name ######\n");
    getword(word, MAXWORD);
    root = deletenode(root, word);

    fprintf(stdout, "# after delete, tree print ######\n");
    treeprint(root);

    alldeletenode(root);

    return 0;
}

tnode_t *addnode(tnode_t *p, char *w)
{
    int cond;
    if (NULL == p) {
        p = talloc();
        p->word = strdup(w);
        p->left = p->right = NULL;
    } else if ((cond = strcmp(w, p->word)) == 0) {
        /* print error, cannot insert same word */
        fprintf(stderr, "Error! same word\n\n");
    } else if (cond < 0) {
        p->left = addnode(p->left, w);
    } else {
        p->right = addnode(p->right, w);
    }

    return p;
}

tnode_t * getnode(tnode_t *p, tnode_t **prev, const char *word)
{
    int cond = 0;
    while (p) {
        cond = strcmp(word, p->word);
        if (cond < 0) {
            *prev = p;
            p = p->left;
        } else if (cond > 0) {
            *prev = p;
            p = p->right;
        } else {
            break;
        }
    } 
    return p;
}

tnode_t * deletenode(tnode_t *p, char *w)
{
    tnode_t *deleted, *d_parent, *move, *m_parent; 
    deleted = NULL;
    d_parent = NULL;
    move = NULL;
    m_parent = NULL;

    deleted = getnode(p, &d_parent, w);

    if (!d_parent && !deleted) {
        fprintf(stderr, "[Error] empty tree, add node first.\n");
        return p;
    } else if (d_parent && !deleted) {
        fprintf(stderr, "[Failed] cannot found node.(word:\"%s\")\n", w);
        return p;
    }

    move = getreplace(deleted, &m_parent);

    if (m_parent == deleted) {
        if (move == m_parent->left)
            move->right = deleted->right; 
        else
            move->left = deleted->left; 
    } else if (m_parent != NULL) {
        if (move == m_parent->left) {
            m_parent->left = move->right; 
        } else {
            m_parent->right = move->left; 
        }
        move->right = deleted->right; 
        move->left = deleted->left; 
    }

    if (d_parent) {
        if (d_parent->left == deleted) {
            if (deleted == move)
                d_parent->left = NULL;
            else 
                d_parent->left = move;
        } else if (d_parent->right == deleted) {
            if (deleted == move)
                d_parent->right = NULL;
            else 
                d_parent->right = move;
        }
    } else {
        p = move;
    }

    if (deleted)
        freenode(deleted);

    return p;
}

tnode_t * getreplace(tnode_t *move, tnode_t **parent)
{
    if (move->left) {
        *parent = move;
        move = move->left;
        while (move->right) {
            *parent = move;
            move = move->right;
        }
    } else if (move->right) {
        *parent = move;
        move = move->right;
        while (move->left) {
            *parent = move;
            move = move->left;
        }
    }
    return move;
}


void treeprint(tnode_t *p)
{
    if (p) {
        treeprint(p->left);
        fprintf(stdout, "%s ", p->word);
        treeprint(p->right);
    }
}

tnode_t * talloc(void)
{
    return (tnode_t *)malloc(sizeof(tnode_t));
}

void freenode(tnode_t *p)
{
    if (p->word)
        free(p->word);

    if (p)
        free(p);
}

char * strdup(char *s)
{
    char *p;
    p = (char *)malloc(strlen(s)+1);
    memset(p, 0x00, strlen(s)+1);
    if (p != NULL)
        strcpy(p, s);
    return p;
}

int getword(char *s, int len)
{
    int i = 0;
    char ch = 0;

    memset(s, 0x00, len);
    while ('\n' != (ch = getchar()) && i < len) {
        s[i++] = ch;
    }
    return 0;
}

void alldeletenode(tnode_t * p)
{
    if (p) {
        alldeletenode(p->left);
        alldeletenode(p->right);
        freenode(p);
    }
}
