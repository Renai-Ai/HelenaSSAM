# HelenaSSAM
Helena -- a Small Shape Action Model

## Latest Updates

We will update this section when our 2024 effort commences.

## Getting Started

## Introduction

HelenaSSAM is an open source language or action model with the following goals.

1. The system shall translate from human languge commands to computer aided design (CAD) action sequences.
2. The sequence shall be runnable in a To Be Decided CAD system such as CADQuery, FreeCAD, OnShape, Fusion360, or Blender.
3. The model shall fit (for inference) in a computer with relatively small specifications as defined below (e.g. memory of 32 GB, and a single GPU). The output shall be computable in 30 seconds or less.
4. Training the system shall be feasible in a computer with similar specifications or a small cluster, e.g. with 5 computers, of similar specifications. Training the model can take longer (e.g. 1 month).

## Example of input and output

User: `could you help me create a 3d model of a hammer`

HelenaSSAM: [A sequence of CAD operations that results in a 3d model for a hammer] 

## What is a _small_ model?

We are defining a small computer as a computing device that is readily avaiable off the shelf for less than about US$3,000 at any given time and that requires less thatn 1,000 Watts of power to run on average. As of this writing in 2024, this is likely not a mobile device like a phone. It could be a laptop device, but is more likely a desktop computer with a GPU installed. 

The state of the art for 3D model generation from text is really bad. So, we beleive we can create a reasonable model that is better than the state of art with a restricted input set of everyday 3d objects. Examples of everyday 3d objects for which training data are readily avaiable include tools such as hammers, drills; furniture such as chairs, tables; and vehicles such as different types of cars, aircraft, etc.

## Why do we call it an _action_ model and not just a _language_ model?

Let's take the example of robotic motion plannin. Going from a description of intended goal such as ``Transfer the dishes from the table to the sink`` does not have one single path to actual motor sequence of actions performed by a robot. It could need feedback from the real world to adjust its initial plan based on feedback from the real world.

When complete, we imagine that Helena will be able to interact with various CAD tools through API-like machine-to-machine software interfaces. Versions of different CAD design tools might be able to provide new operations that the model can try and get partial output. The model chould change or undo operations to get to the final CAD result.

For an initial version of the model, we will assume that the model will generate the whole sequence in one go without feedback. In that sense, it will be a language model where the input will be human language and the ouput will be a CAD sequence.

## What does the name Helena stand for?

This project was started at Renaissance Ai (a Simulate Anything, Inc. company). We are a Boston, MA, USA based startup with founders from MIT and Harvard. Our logo is a representation of a Hummingbird as we were thinking that we should be able to create AI that can engineer designs as efficient and sophisticated as a hummingbird.

We have been choosing project names based on types of hummingbirds. Helena is a type of hummingbird. 

## Architecture

For an initial version, we start out with a DALL-E-2 like architecture combined with the approach in [DeepCAD](https://github.com/ChrisWu1997/DeepCAD) of mapping embedding vectors to CAD sequences.

For the codebase, we start with the code in an [open source PyTorch implementation of DALL-E-2](https://github.com/lucidrains/DALLE2-pytorch).

### Nearterm 2024 Research Questions

Questions to be answered:

1. Do all vectors in the embedding space used in DeepCAD result in a valid CAD sequence?

2. How does [CLIP](https://openai.com/index/clip/) work with CAD sequence outputs?

3. Is there a way to use a larger dataset of CAD models where the sequence is not avaiable and backtrack the sequence similar to how DeepCAD dataset was derived from ABC dataset. However, for the DeepCAD dataset, we believe the source OnShape database was avaiable and this mapping would not have been simple without this source.

## Data

We start out with the data from the [DeepCAD](https://github.com/ChrisWu1997/DeepCAD) (which is derived from the [ABC CAD dataset](https://archive.nyu.edu/handle/2451/43778)), and labels from the ABC dataset. However, the labels in this dataset are relatively of low quality. Renaissance Ai is working on a different higher quality dataset that could be used in the future for refined models.

## Team 2024

In 2024, the starting team for V0 of HelenaSSAM is the Renaissance Ai team and a team from [MIT Break Through Tech AI](https://computing.mit.edu/about/diversity-equity-inclusion/break-through-tech-ai/).

### Renaissance Ai team members

- Prakash Manandhar
- Sansar Jung Dewan
- Saugat Paudel
- Sue Manandhar
- Aakansh Thapa

### Break Through Tech AI team members

- Divya V. Nori
- Larissa Zhu
- Lesly Gonzalez Herrera
- Manik Sharma
- Rachel Reinking
- Shiven Patel
