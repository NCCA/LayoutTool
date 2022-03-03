# Layout Tool 

Basic idea
1. 2D layout tool using grid to put 3D assets into scene.
2. Assets are chosen from Database
3. Placed in grid
4. Need to store this data to file, may need various criteria for asset
5. Ability to load these files into a DCC (scene file)
6. Grouping ability?
7. User scattering, (Brushes etc)

# Data

## Assets (A database)

Dimensions, Name (Description), File Format (Obj,Rib,Alembic,HIP,MA) ID? Picture(s)
Show (Is it general re-usable), Buildings, landscape, set dressing Taxonomy (What is it?)
Shot.  location. (Asset Key Unique ID)

## Scene JSON scene files.

Grid for scene (is it layered?) Dimensions (W/D/step) Are we using real units or not?

Cells -> What is in a Cell? Asset (Instance or copy?) Asset key can add colour for visualisation. 

This will map to a 3D transform, may have tool store and allow this to be modified. 

{
  "SceneData" :{
          "Width" : [100],
          "Depth" : [100]
  },
  "AppData" :{

  }
}






















